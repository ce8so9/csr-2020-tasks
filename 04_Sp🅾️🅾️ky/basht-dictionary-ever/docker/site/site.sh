#!/bin/bash

. /site/config.sh

printf "[C] %s:%d\n" "${SOCAT_PEERADDR}" "${SOCAT_PEERPORT}" >&2

read -t 1 -r head || exit 0
printf "[F] %s\n" "$(echo "${head}" | tr -d '\r\n')" >&2
method="$(echo "${head}" | cut -d' ' -f1)"
path="$(echo "${head}" | cut -d' ' -f2 | cut -d'?' -f1)"
query="$(echo "${head}" | cut -d' ' -f2 | cut -d'?' -f2-)"
http="$(echo "${head}" | cut -d' ' -f3)"

while true; do
	read -r line
	line="$(echo "${line}" | tr -d '\r\n')"
	[ -n "${line}" ] || break

	varname="$(echo "${line}" | awk -F ': ' '{print $1}' | sed -e 's/[^[:alnum:]]/-/g' | tr -d '-' | tr A-Z a-z)"
	value="$(echo "${line}" | awk -F ': ' '{print $2}')"

	export -- "http_${varname}=${value}"
done

output=""

_magic() {
	case "${1}" in
		"ico") printf "image/vnd.microsoft.icon";;
		"png") printf "image/png";;
		"css") printf "text/css";;
		"html") printf "text/html; charset=utf-8";;
		"js") printf "text/javascript";;
		*) printf "text/plain";;
	esac
}

if [ "${path: -1}" = "/" ]; then
	path="${path}index.html"
fi

for file in $(find /site/static/ -type f); do
	if [ "${file:12}" = "${path}" ]; then
		ext="$(echo "${path}" | rev | cut -d'.' -f1 | rev)"
		printf "HTTP/1.1 200 OK\r\n"
		printf "Server: socat+bash/0.0.1a\r\n"
		printf "Connection: close\r\n"
		printf "Content-Type: %s\r\n" "$(_magic "${ext}")"
		printf "Expires: Sat, 01 Jan 2022 00:00:00 GMT\r\n"
		printf "Last-Modified: Mon, 08 Dec 2014 19:23:51 GMT\r\n"
		printf "Cache-Control: max-age=222928569\r\n"
		if [ "${ext}" = "html" ]; then
			filelen="$(wc -c "${file}" | cut -d' ' -f1)"
			headerlen="$(wc -c "/site/templates/header.tpl" | cut -d' ' -f1)"
			footerlen="$(wc -c "/site/templates/footer.tpl" | cut -d' ' -f1)"
			printf "Content-Length: %d\r\n" "$((headerlen+filelen+footerlen))"
			printf "\r\n"
			cat "/site/templates/header.tpl" "${file}" "/site/templates/footer.tpl"
		else
			printf "Content-Length: %d\r\n" "$(wc -c "${file}" | cut -d' ' -f1)"
			printf "\r\n"
			cat "${file}"
		fi
		exit 0
	fi
done

if [ "${path}" = "/api" ] && [ "${http_authorization}" = "${TOKEN}" ]; then
	read -r query
	query="$(echo "${query}" | tr -d '\r\n')"
	printf "[A] %s\n" "$(echo "${query}" | tr -d '\r\n')" >&2
	ret="$(env "${query}" /site/query.sh)"
	printf "HTTP/1.1 418 I'm a teapod, but that's okay\r\n"
	printf "Server: socat+bash/0.0.1a\r\n"
	printf "Connection: close\r\n"
	printf "Content-Type: text/html\r\n"
	printf "Content-Length: %d\r\n" "$(printf -- "${ret}" | wc -c )"
	printf "\r\n"
	printf "%s" "${ret}"
	exit 0
fi

if [ "${path}" = "/search.html" ]; then
	search="$(echo "${query}" | awk -F '(^|&)query=' '{print $2}' | sed -e 's/[^[:alnum:]]/-/g' | tr -d '-' | tr A-Z a-z)"
	if [ -n "${search}" ]; then
		content="$(curl -s -H "Authorization: ${TOKEN}" -d "query=${search}"$'\r\n' "http://127.0.0.1:9256/api")"
	else
		content=""
	fi

	filelen="$(wc -c "/site/templates/search.tpl" | cut -d' ' -f1)"
	headerlen="$(wc -c "/site/templates/header.tpl" | cut -d' ' -f1)"
	footerlen="$(wc -c "/site/templates/footer.tpl" | cut -d' ' -f1)"
	contentlen="$(printf -- "${content}" | wc -c)"
	printf "HTTP/1.1 200 OK\r\n"
	printf "Server: socat+bash/0.0.1a\r\n"
	printf "Connection: close\r\n"
	printf "Content-Type: text/html\r\n"
	printf "Content-Length: %d\r\n" "$((headerlen+filelen+contentlen+footerlen))"
	printf "\r\n"
	cat "/site/templates/header.tpl" "/site/templates/search.tpl"
	printf -- "${content}"
	cat "/site/templates/footer.tpl"
	exit 0
fi

printf "HTTP/1.1 404 Not Found\r\n"
printf "\r\n"
printf "File not found :("
