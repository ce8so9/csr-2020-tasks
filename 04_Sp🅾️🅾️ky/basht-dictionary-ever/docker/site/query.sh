#!/bin/bash

echo '</main><main role="main" class="container">'
echo '<div class="my-3 p-3 bg-white rounded box-shadow">'
echo '<h6 class="border-bottom border-gray pb-2 mb-0">Search results</h6>'

i=0
grep -i "${query}" /site/words.txt | head -n 20 | while read line; do
	i=$((i+1))
	echo '<div class="media text-muted pt-3">'
	echo '<p class="media-body pb-3 mb-0 small lh-125 border-bottom border-gray">'
	echo '<strong class="text-gray-dark">'${i}'</strong>'
	echo "$(echo "${line}" | tr -d '\r\n')"
	echo '</p>'
	echo '</div>'
done
