export dump=plwiki.json.gz
export index=poleval
mkdir chunks
cd chunks
zcat < ../$dump | split -a 10 -l 500 - $index

