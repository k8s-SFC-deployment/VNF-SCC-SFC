EXTERNAL_URL=<host-domain>:<node-port>
FIRST_REQUEST_URL=${EXTERNAL_URL}/firewall/load
FIRST_REQUEST_PARAM_TRANSMITTINGLOAD=$(urlencode '{"mb": 10}')
FIRST_REQUEST_PARAM_NEXT=$(urlencode '{"target_url":"http://firewall-vnf.testbed.svc/firewall/load","message": {"processingLoad": {"cpu_core": 1,"percentage": 70,"mem_mb": 512,"duration_sec": 20},"transmittingLoad": null,"next": {"target_url": "http://ids-vnf.testbed.svc/ids/load","message": null}}}')

FIRST_REQUEST=${FIRST_REQUEST_URL}?transmittingLoad=${FIRST_REQUEST_PARAM_TRANSMITTINGLOAD}\&next=${FIRST_REQUEST_PARAM_NEXT}

while true; do
  curl -X 'POST' \
  $FIRST_REQUEST \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@README.md'
done

# {"mb": 10}
# {
#   "target_url":"http://firewall-vnf.testbed.svc/firewall/load",
#   "message": {
#     "processingLoad": {
#       "cpu_core": 1,
#       "percentage": 70,
#       "mem_mb": 512,
#       "duration_sec": 10
#     },
#     "transmittingLoad": null,
#     "next": {
#       "target_url": "http://ids-vnf.testbed.svc/ids/load",
#       "message": null
#     }
#   }
# }


