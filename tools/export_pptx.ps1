# Exporte le PPTX en PDF et en images PNG (une par slide) via PowerPoint.
# Usage : powershell -File tools\export_pptx.ps1 [-Pptx <chemin>] [-PngDir <dossier>]
param(
    [string]$Pptx   = "FINAL_SOUTENANCE\Travelling_Merchant_Romain_Yannis_Lisa_FINAL.pptx",
    [string]$Pdf    = "FINAL_SOUTENANCE\Travelling_Merchant_Romain_Yannis_Lisa_FINAL.pdf",
    [string]$PngDir = ""
)

$ErrorActionPreference = "Stop"
$root = (Get-Location).Path
$pptxPath = Join-Path $root $Pptx
$pdfPath  = Join-Path $root $Pdf

if (-not (Test-Path $pptxPath)) { throw "Introuvable : $pptxPath" }

$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open($pptxPath, $true, $false, $false)   # ReadOnly, no window

# 32 = ppSaveAsPDF
$pres.SaveAs($pdfPath, 32)
Write-Output "PDF   : $pdfPath"

if ($PngDir -ne "") {
    $pngPath = Join-Path $root $PngDir
    if (-not (Test-Path $pngPath)) { New-Item -ItemType Directory -Force $pngPath | Out-Null }
    Get-ChildItem $pngPath -Filter "slide*.png" -ErrorAction SilentlyContinue | Remove-Item -Force
    # 18 = ppSaveAsPNG ; largeur/hauteur en pixels
    $pres.SaveCopyAs($pngPath, 18)
    Write-Output "PNG   : $pngPath"
}

$pres.Close()
$ppt.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null
Write-Output "OK"
