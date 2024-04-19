make_message () {
    cd $1
    django-admin makemessages -l $2
    cd ..
}

compile_messages () {
    cd $1
    django-admin compilemessages
    cd ..
}

apps=(abiturient1 abiturients university_offers documents accepting_offers users_login pk_panel)
langs=(en uk)

if [[ "$1" == "make" ]]; then
    for lang in ${langs[@]}; do
        for app in ${apps[@]}; do
            make_message $app $lang
        done
    done
elif [[ "$1" == "compile" ]]; then
    for app in ${apps[@]}; do
        compile_messages $app
    done
fi
