export HASURA_ADMIN_SECRET='<secreto-prod>'
cd ~/aranea/work/echo-prod-rollout-20260925/release/hasura
./cli-hasura metadata export --endpoint http://192.168.31.48:8080 --admin-secret "$HASURA_ADMIN_SECRET" -o json > backup-prod-meta.json
python3 merge_metadata.py backup-prod-meta.json metadata merged.json
HASURA_ADMIN_SECRET="$HASURA_ADMIN_SECRET" ./apply_merged.sh merged.json