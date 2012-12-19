$(function() {
    var tree = LSO.d3.formTree()
        .height(100)
        .data({
            name: 'bhU',
            children: [
                {
                    name: 'bhava',
                    children: [
                        { name: 'bhavati' },
                        { name: 'bhavate' }
                    ]
                }
            ]
        });
    tree('#bhu-present');
});