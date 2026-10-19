// G1 harness: reconstructs the effective production Builder overview-producer
// configuration using the VERBATIM 0.3.1 (492a271e) functions extracted from
// sqx/activities/worker/steps/steps.go. Deviations from the worker path are
// limited to: capabilities.ErrContractConflict -> local sentinel and
// runtime.IsWatcherImportCohortHop -> stub (builder path under test).
package main

import (
	"archive/zip"
	"bytes"
	"encoding/xml"
	"errors"
	"fmt"
	"io"
	"os"
	"strings"
)

var ErrContractConflict = errors.New("contract conflict")

type fakeTask struct{}

func (fakeTask) watcherImport() bool { return false }

// ---------------- verbatim block from 492a271e ----------------

func overviewCustomAnalysisTaskXML(plugin, inputDatabank string) []byte {
	return []byte(fmt.Sprintf(`<Settings>
  <CustomAnalysis>
    <PerStrategy1>none</PerStrategy1>
    <PerStrategy2>none</PerStrategy2>
    <FullDatabank1>%s</FullDatabank1>
    <FullDatabank2>none</FullDatabank2>
    <RemoveFailedStrategies>false</RemoveFailedStrategies>
    <Filter>false</Filter>
    <InputArgsPerStrategy1 />
    <InputArgsPerStrategy2 />
    <InputArgsFullDatabank1 />
    <InputArgsFullDatabank2 />
  </CustomAnalysis>
  <Databanks>
    <Databank label="Input databank" name="Input" value="%s" />
    <Databank label="Output databank" name="Output" value="output" />
  </Databanks>
  <CrossChecks>
    <RetestOnAdditionalMarkets />
    <WhatIf />
    <MonteCarloManipulation />
    <MonteCarloRetest />
    <OptProfileSysParamPermutation />
    <WalkForwardOptimization />
    <WalkForwardMatrix />
    <SequentialOptimization />
    <RetestWithHigherPrecision />
  </CrossChecks>
  <Resources>
    <Symbols />
    <Brokers />
    <Instruments />
    <Sessions />
    <CustomIndicators />
    <CustomBlocks />
  </Resources>
</Settings>
`, plugin, inputDatabank))
}

func ensureProjectOverviewProducer(configContent []byte, otherFiles map[string][]byte, plugin, inputDatabank string) ([]byte, error) {
	if strings.TrimSpace(plugin) == "" {
		return nil, fmt.Errorf("durable builder: overview producer plugin is empty: %w", ErrContractConflict)
	}
	if strings.TrimSpace(inputDatabank) == "" {
		return nil, fmt.Errorf("durable builder: overview producer input databank is empty: %w", ErrContractConflict)
	}
	var project cfxProject
	if err := xml.Unmarshal(configContent, &project); err != nil {
		return nil, fmt.Errorf("durable builder: invalid Project config.xml: %w", err)
	}
	var customAnalysisFiles []string
	for _, task := range project.Tasks.Task {
		if strings.EqualFold(strings.TrimSpace(task.Type), "CustomAnalysis") {
			customAnalysisFiles = append(customAnalysisFiles, strings.TrimSpace(task.TaskXMLFile))
		}
	}
	if len(customAnalysisFiles) > 1 {
		return nil, fmt.Errorf("durable builder: duplicate CustomAnalysis tasks: %w", ErrContractConflict)
	}
	if len(customAnalysisFiles) == 1 {
		fileName := customAnalysisFiles[0]
		content, ok := otherFiles[fileName]
		if !ok || !strings.Contains(string(content), plugin) {
			return nil, fmt.Errorf("durable builder: existing CustomAnalysis producer conflicts with %q: %w", plugin, ErrContractConflict)
		}
		bound, err := bindOverviewProducerInputDatabank(content, inputDatabank)
		if err != nil {
			return nil, err
		}
		otherFiles[fileName] = bound
		return configContent, nil
	}

	taskFile := "CustomAnalysis-Task1.xml"
	for i := 2; ; i++ {
		if _, exists := otherFiles[taskFile]; !exists {
			break
		}
		taskFile = fmt.Sprintf("CustomAnalysis-Task%d.xml", i)
	}
	closeTasks := strings.LastIndex(string(configContent), "</Tasks>")
	if closeTasks < 0 {
		return nil, fmt.Errorf("durable builder: Project config.xml has no Tasks section: %w", ErrContractConflict)
	}
	fragment := fmt.Sprintf("  <Task name=\"Custom analysis\" type=\"CustomAnalysis\" taskXMLFile=\"%s\" active=\"true\" />\n", taskFile)
	updated := make([]byte, 0, len(configContent)+len(fragment))
	updated = append(updated, configContent[:closeTasks]...)
	updated = append(updated, fragment...)
	updated = append(updated, configContent[closeTasks:]...)
	otherFiles[taskFile] = overviewCustomAnalysisTaskXML(plugin, inputDatabank)
	return updated, nil
}

func bindOverviewProducerInputDatabank(content []byte, databank string) ([]byte, error) {
	decoder := xml.NewDecoder(bytes.NewReader(content))
	var output bytes.Buffer
	encoder := xml.NewEncoder(&output)
	matched := 0

	for {
		token, err := decoder.Token()
		if err == io.EOF {
			break
		}
		if err != nil {
			return nil, fmt.Errorf("durable builder: invalid CustomAnalysis XML: %w", err)
		}
		if start, ok := token.(xml.StartElement); ok && strings.EqualFold(start.Name.Local, "Databank") {
			name, label := "", ""
			for _, attr := range start.Attr {
				switch strings.ToLower(attr.Name.Local) {
				case "name":
					name = strings.TrimSpace(attr.Value)
				case "label":
					label = strings.TrimSpace(attr.Value)
				}
			}
			if strings.EqualFold(name, "Input") || strings.EqualFold(label, "Input databank") {
				matched++
				hasValue := false
				for i := range start.Attr {
					if strings.EqualFold(start.Attr[i].Name.Local, "value") {
						start.Attr[i].Value = databank
						hasValue = true
						break
					}
				}
				if !hasValue {
					start.Attr = append(start.Attr, xml.Attr{Name: xml.Name{Local: "value"}, Value: databank})
				}
			}
		}
		if err := encoder.EncodeToken(token); err != nil {
			return nil, fmt.Errorf("durable builder: encode CustomAnalysis XML: %w", err)
		}
	}
	if err := encoder.Flush(); err != nil {
		return nil, fmt.Errorf("durable builder: flush CustomAnalysis XML: %w", err)
	}
	if matched != 1 {
		return nil, fmt.Errorf("durable builder: CustomAnalysis input databank binding count=%d, want 1: %w", matched, ErrContractConflict)
	}
	return output.Bytes(), nil
}

type cfxProject struct {
	Tasks struct {
		Task []struct {
			Type        string `xml:"type,attr"`
			TaskXMLFile string `xml:"taskXMLFile,attr"`
		} `xml:"Task"`
	} `xml:"Tasks"`
}

func overviewProducerInputDatabank(task fakeTask) string {
	if task.watcherImport() {
		return "input"
	}
	return "output"
}


// ---------------- harness driver ----------------

const baseProject = `<Project name="custom" version="142.2399">
  <Tasks>
  </Tasks>
  <Databanks>
    <Databank name="Results" view="Default - Main data" syncType="Auto-sync never" position="10" />
    <Databank name="input" view="Default - Main data" syncType="Auto-sync every 1 hour" position="200" />
    <Databank name="output" view="Default - Main data" syncType="Auto-sync every 1 hour" position="105" />
  </Databanks>
</Project>
`

func main() {
	otherFiles := map[string][]byte{}
	updated, err := ensureProjectOverviewProducer([]byte(baseProject), otherFiles, "EchoForgeOverviewExporter", overviewProducerInputDatabank(fakeTask{}))
	if err != nil {
		panic(err)
	}
	f, err := os.Create("project.cfx")
	if err != nil {
		panic(err)
	}
	defer f.Close()
	zw := zip.NewWriter(f)
	cf, err := zw.Create("config.xml")
	if err != nil {
		panic(err)
	}
	if _, err := cf.Write(updated); err != nil {
		panic(err)
	}
	for _, name := range []string{"CustomAnalysis-Task1.xml"} {
		w, err := zw.Create(name)
		if err != nil {
			panic(err)
		}
		if _, err := w.Write(otherFiles[name]); err != nil {
			panic(err)
		}
	}
	if err := zw.Close(); err != nil {
		panic(err)
	}
	os.WriteFile("config.xml.out", updated, 0o644)
	os.WriteFile("CustomAnalysis-Task1.xml.out", otherFiles["CustomAnalysis-Task1.xml"], 0o644)
	_, _ = os.Stdout.WriteString(string(otherFiles["CustomAnalysis-Task1.xml"]))
	_ = strings.TrimSpace("")
	_ = bytes.MinRead
	_ = xml.Header
	_ = fmt.Sprint()
}
