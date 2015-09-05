$(function() {
    var tree = LSO.d3.formTree()
        .height(200)
        .data({
            name: 'bhU',
            children: [
                {
                    name: 'bhava',
                    children: [
                        { name: 'bhavati' },
                        { name: 'bhavate' }
                    ],
                },
                {
                    name: 'bhUya',
                    children: [
                        { name: 'bhUyate' }
                    ]
                }
            ]
        });
    tree('#bhu-present');
});
