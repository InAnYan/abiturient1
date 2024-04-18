$applications = "abiturient1", "persons", "accepting_offers", "documents", "university_offers"
$languages = "en", "uk"

function Change-DirectorySafely ($path) {
    if (Test-Path $path)  {
        Set-Location $path
    } else {
        Write-Error "Directory not found: $path"
    }
}

function Create-DirectoryIfNotExists {
    Param(
        [Parameter(Mandatory)]
        [string]$Path
    )

    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force
    }
} 

if ($args.Count -ne 1) {
    Write-Error "Usage: ./MakeMessages.ps1 [make|compile]"
    exit 1
}

$action = $args[0]
if ($action -notin "make", "compile") {
    Write-Error "Invalid argument. Use 'make' or 'compile'"
    exit 2
}

if ($action -eq "make") {
    foreach ($language in $languages) {
        foreach ($app in $applications) {
            Change-DirectorySafely $app

            Create-DirectoryIfNotExists locale

            django-admin makemessages -l $language

            cd .. 
        }
    }
} else {
    foreach ($app in $applications) {
        Change-DirectorySafely $app

        django-admin compilemessages

        cd .. 
    }
}
