package main

import (
	"context"
	"fmt"
	"log"

	"go.temporal.io/sdk/client"
	"go.temporal.io/sdk/worker"
	"go.temporal.io/api/enums/v1"
	historypb "go.temporal.io/api/history/v1"
	"github.com/xKoRx/sdk/pkg/shared/etcd"
	"github.com/xKoRx/sdk/pkg/shared/telemetry"
	"github.com/xKoRx/symphony/internal/di"
	"github.com/xKoRx/symphony/sqx/workflows"
)

type replayEtcd struct{}
func (*replayEtcd) Get(string)(string,bool){return "",false}
func (*replayEtcd) SetVar(context.Context,string,string)error{return nil}
func (*replayEtcd) Close()error{return nil}
func (*replayEtcd) Reload()error{return nil}
func (*replayEtcd) WatchKey(context.Context,string)(<-chan etcd.WatchEvent,error){return make(chan etcd.WatchEvent),nil}
func (*replayEtcd) WatchPrefix(context.Context,string)(<-chan etcd.WatchEvent,error){return make(chan etcd.WatchEvent),nil}

func main(){
	di.Container.Telemetry=&telemetry.Client{};di.Container.Etcd=&replayEtcd{}
	c,err:=client.Dial(client.Options{HostPort:"192.168.31.46:7233",Namespace:"sqx-prop"});if err!=nil{log.Fatal(err)};defer c.Close();ctx:=context.Background()
	items:=[][3]string{{"wave1","sqx-main-v1-1656f4f7-2ebe-4aee-ae71-9571510976b3","01a071b2-ee84-78da-bb84-e01160b0f9ba"},{"wave2","sqx-main-v1-592d2709-877b-4927-a6a2-b3db70ff1737","01a071b7-cfa4-7c0c-b44a-99de566d732d"}}
	for _,x:=range items{it:=c.GetWorkflowHistory(ctx,x[1],x[2],false,enums.HISTORY_EVENT_FILTER_TYPE_ALL_EVENT);h:=&historypb.History{};for it.HasNext(){e,e2:=it.Next();if e2!=nil{log.Fatal(e2)};h.Events=append(h.Events,e)};r:=worker.NewWorkflowReplayer();r.RegisterWorkflow(workflows.GenericSQXWorkflow);r.RegisterWorkflow(workflows.GroupSQXWorkflow);r.RegisterWorkflow(workflows.MT5CompileArtifactWorkflow);r.RegisterWorkflow(workflows.MT5BacktestArtifactWorkflow);if err:=r.ReplayWorkflowHistory(nil,h);err!=nil{fmt.Printf("REPLAY|%s|FAIL|%v\n",x[0],err)}else{fmt.Printf("REPLAY|%s|PASS|events=%d\n",x[0],len(h.Events))}}
}
