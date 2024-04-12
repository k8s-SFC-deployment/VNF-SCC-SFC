{{/*
Expand the name of the chart.
*/}}
{{- define "vnf-scc-sfc.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "vnf-scc-sfc.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "vnf-scc-sfc.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "vnf-scc-sfc.labels" -}}
helm.sh/chart: {{ include "vnf-scc-sfc.chart" . }}
{{ include "vnf-scc-sfc.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "vnf-scc-sfc.selectorLabels" -}}
app.kubernetes.io/name: {{ include "vnf-scc-sfc.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Environments
*/}}
{{- define "vnf-scc-sfc.envs" -}}
{{- range $key, $val := .Values.envs }}
- name: {{ $key }}
  value: "{{ $val }}"
{{- end }}
{{- if not .Values.envs.ROOT_PATH }}
- name: ROOT_PATH
  value: "/{{ include "vnf-scc-sfc.fullname" . }}"
{{- end }}
{{- end }}
