$givenURL = "http://visionfromabove.co.uk/"
#$givenURL = "https://glasswallsolutions.com/"
$sitename = ([System.Uri]$givenURL).Host -replace '^www\.'
$outputedFilesDirectory = "C:\site\mirror"
$parentPath = "C:\output\single\"

docker run -it -v C:/site:/app -e HTTRACK_URI=$givenURL ralfbs/httrack:latest


New-Item -ItemType directory (Join-Path $parentPath $sitename)

$sourcepath = "C:\site\mirror\" 
$destination = "C:\output\single\" + $sitename
$sourcefiles = get-childitem $sourcepath  -file -Recurse

foreach ($file in $sourcefiles) {
Copy-Item $file.FullName -Destination "$destination\$($file.Name)"
}

Remove-Item -Path $mirror* -recurse


#need to implement folder creation, and ability to pass in website url to the script 