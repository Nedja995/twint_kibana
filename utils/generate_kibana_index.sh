#/bin/bash
# THIS IS REFERENCE FOR FUTURE UPGRADES

if [[ $# -eq 0 ]] ; then
    echo "Usage: `basename "$0"` <Kibana-URL> [noauth]" 
	echo "Example: `basename "$0"` http://localhost:5601"
    exit 1
fi

AUTH=""
if [[ "$2" != "noauth" ]]; then
	echo "Please enter your username..."
	read  KIBANAUSER
	echo "Please enter your password..."
	read -s KIBANAPASSWORD
	AUTH="-u $KIBANAUSER:$KIBANAPASSWORD"
fi

KIBANASERVER=$1
INDEXPATH="es_admin/.kibana/index-pattern"
DEFAULTINDEX="logstash-*"
PATTERNS="logstash-*
logstash-foo-*
logstash-bar-*"

#Creating Index Patterns
while IFS= read -r PATTERN 
do 
  PAYLOAD='{"title":"${PATTERN}","timeFieldName":"@timestamp"}'
  echo ""
  echo "#### CREATING INDEX PATTERN ${PATTERN}... ####"
  curl ${KIBANASERVER}/${INDEXPATH}/${PATTERN}/_create   -H "Content-Type: application/json" -H "Accept: application/json, text/plain, */*" -H "kbn-xsrf: anything" --data-binary ${PAYLOAD} -u ${KIBANAUSER}:${KIBANAPASSWORD}  -w "\n" # append this for debugging (it will log your password!!) : -v --libcurl dump.txt
done <<< "$PATTERNS"

#Setting default Index
# DEFAULTINDEXPAYLOAD="{\"value\":\"${DEFAULTINDEX}\"}"
# echo ""
# echo "#### SETTING DEFAULT INDEX TO ${DEFAULTINDEX} ####"
# curl ${KIBANASERVER}/api/kibana/settings/defaultIndex   -H "Content-Type: application/json" -H "Accept: application/json, text/plain, */*" -H "kbn-xsrf: anything" -H "Connection: keep-alive" --data-binary ${DEFAULTINDEXPAYLOAD} ${AUTH}  -w "\n" --compressed 