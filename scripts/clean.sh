sed -i 's:<p>::' $1
sed -i 's:</p>::' $1
sed -i 's:<strong>:**:' $1
sed -i 's:</strong>:**:' $1
sed -i 's:<em>:*:' $1
sed -i 's:</em>:*:' $1
sed -i -e 's:<h2>\(.*?\)</h2>:## \1:' $1
sed -i -e 's:<ul class="examples">:!!! examples:' $1
sed -i -e 's:</ul>::' $1
sed -i -e "s:.*{{ ex(\(.*?\)) }}:    - {{ m.x(\1) }}:" $1
sed -i -e "s:.*{{ '\(.*?\)'|i }}:\`\1\`:" $1
