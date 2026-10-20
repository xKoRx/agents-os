{

"mcp": {

"servers": {

"aranea-ssh": {

"type": "http",

"url": "http://mcps.lab.aranea.cl:3000/",

"headers": {

"Authorization": "Bearer d4e484b5491e5e0c9240264a612b96dd0663d15483c4da434d12385bb3d59f33"

}

},

"aranea-postgres-ro": {

"type": "http",

"url": "http://mcps.lab.aranea.cl:3001/mcp",

"headers": {

"Authorization": "Bearer 31004ba22be813ae9f23f2ebb2695f4a520880a76e493b69138e8677584c6b6a"

},

"enabled": true

},

"aranea-postgres-rw": {

"type": "http",

"url": "http://mcps.lab.aranea.cl:3002/mcp",

"headers": {

"Authorization": "Bearer 3d29abc7f8c0318b81a030da11d4a43bc26a3ceb9ebfda3c2de7ba13e8385ebc"

},

"enabled": true

},

"aranea-mongo-forge-ro": {

"type": "http",

"url": "http://mcps.lab.aranea.cl:3003/mcp",

"headers": {

"Authorization": "Bearer 31004ba22be813ae9f23f2ebb2695f4a520880a76e493b69138e8677584c6b6a"

},

"enabled": true

},

"aranea-mongo-forge-rw": {

"type": "http",

"url": "http://mcps.lab.aranea.cl:3004/mcp",

"headers": {

"Authorization": "Bearer 3d29abc7f8c0318b81a030da11d4a43bc26a3ceb9ebfda3c2de7ba13e8385ebc"

},

"enabled": true

},

"aranea-hasura-dev-admin": {

"type": "http",

"url": "http://mcps.lab.aranea.cl:3006/mcp",

"headers": {

"Authorization": "Bearer 98222feef6fd941d0708bf64ae928bc996fcebb305ce62b632bcdab1fde10dd2"

},

"enabled": true

},

"aranea-hasura-prod-ro": {

"type": "http",

"url": "http://mcps.lab.aranea.cl:3005/mcp",

"headers": {

"Authorization": "Bearer 037b6f50924c3205d9f4cc19ab2714ff718626c4a1fd7b5ed513acd5f0b655d0"

},

"enabled": true

},

"aranea-kafka-dev-admin": {

"type": "http",

"url": "http://mcps.lab.aranea.cl:3007/mcp",

"headers": {

"Authorization": "Bearer b8970ad70999310a56eb5ac3410e1e1877722ec95db59388761ce2fe8afe7828"

},

"enabled": true

},

"aranea-flink-dev-admin": {

"type": "http",

"url": "http://mcps.lab.aranea.cl:3008/mcp",

"headers": {

"Authorization": "Bearer 9830781395a6b3c1cc9f37925e7f21d40d5efe15052cea23f0ff5399358f4b68"

},

"enabled": true

},

"aranea-observability-ro": {

"type": "http",

"url": "http://mcps.lab.aranea.cl:3009/mcp",

"headers": {

"Authorization": "Bearer 9b10ed2cdbff2364692cf0ec5602b7f92fd44b7b1696a67405f2a5c76af23caf"

},

"enabled": true

},

"aranea-temporal-ro": {

"type": "http",

"url": "http://mcps.lab.aranea.cl:3010/mcp",

"headers": {

"Authorization": "Bearer c4df235b40b707de420acdef4ddf576b5113e4e2309208e2376d6b837c5087e2"

},

"enabled": true

},

"aranea-minio-rw": {

"type": "http",

"url": "http://mcps.lab.aranea.cl:3011/mcp",

"headers": {

"Authorization": "Bearer 5338159c1d57ae72c6015582f1131bf455b495a950a97a3ccccb1c0131cdd95f"

},

"enabled": true

},

"aranea-etcd-ro": {

"type": "http",

"url": "http://mcps.lab.aranea.cl:3012/mcp",

"headers": {

"Authorization": "Bearer fb4ee25be9b83fda1eb0c5410bdcdac536bdaa5c16f4fad4979dabd1e176bac9"

},

"enabled": true

}

}

}

}s