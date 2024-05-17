EXTERNAL_URL=localhost:7000
FIRST_REQUEST_URL=${EXTERNAL_URL}/loadv2
FIRST_REQUEST_PARAM_PROCESSINGLOAD=$(urlencode '{"cpu":{"ops":5000, "worker": 1, "limit": 50}, "mem": {"ops":5000, "worker": 1, "bytes": 10000}, "dio": {"ops":5000, "worker": 1, "bytes": 10000000}}')
# FIRST_REQUEST_PARAM_TRANSMITTINGLOAD=$(urlencode '{"mb": 10}')
FIRST_REQUEST_PARAM_NEXT=$(urlencode '{"target_url": "http://localhost:7000/loadv2","message": {"processingLoad": {"cpu": {"ops": 5000,"worker": 1,"limit": 50},"mem": {"ops": 5000,"worker": 1,"bytes": 10000},"dio": {"ops": 5000,"worker": 1,"bytes": 10000000}},"transmittingLoad": null,"next": {"target_url": "http://localhost:7000/loadv2","message": null}}}')

FIRST_REQUEST=${FIRST_REQUEST_URL}?processingLoad=${FIRST_REQUEST_PARAM_PROCESSINGLOAD}\&next=${FIRST_REQUEST_PARAM_NEXT}

while true; do
  curl -X 'POST' \
  $FIRST_REQUEST \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@README.md'
done


# processingLoad={"cpu":{"ops":5000, "worker": 1, "limit": 50}, "mem": {"ops":5000, "worker": 1, "bytes": 10000}, "dio": {"ops":5000, "worker": 1, "bytes": 10000000}}
# transmittingLoad={"mb": 10}
# next={"target_url": "http://localhost:7000/loadv2","message": {"processingLoad": {"cpu": {"ops": 5000,"worker": 1,"limit": 50},"mem": {"ops": 5000,"worker": 1,"bytes": 10000},"dio": {"ops": 5000,"worker": 1,"bytes": 10000000}},"transmittingLoad": null,"next": {"target_url": "http://localhost:7000/loadv2","message": null}}}

