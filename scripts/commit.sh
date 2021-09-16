menu_from_array ()
{
select item; do

if [ 1 -le "$REPLY" ] && [ "$REPLY" -le $# ];
then
break;
else
echo "Wrong selection ($REPLY): Select any number from 1-$#"
fi
done
}

GITEMOJIS=(':gift:,🎁,Add'
           ':zap:,⚡,Update'
           ':fire:,🔥,Delete'
           ':bug:,🐛,Fix'
           ':gear:,⚙️.,CI'
           ':hammer_and_wrench:,🛠️.,Refactor'
           ':heavy_check_mark:,✔️.,Test'
           ':orange_book:,📙,Docs'
           ':seedling:,🌱,Create')

ITEMS=()
for I in ${GITEMOJIS[@]}; do ITEMS+=("$(echo -n $I | cut --output-delimiter=' ' -d ',' -f 2,3)"); done;
menu_from_array "${ITEMS[@]}"

read -p "$(echo -n ${GITEMOJIS[REPLY-1]} | cut --output-delimiter=' ' -d ',' -f 2,3) " msg

git commit -m "$(echo -n ${GITEMOJIS[REPLY-1]} | cut --output-delimiter=' ' -d ',' -f 1,3) $msg"
