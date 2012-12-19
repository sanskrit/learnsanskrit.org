$(function() {
    var tree = LSO.d3.formTree()
        .height(250)
        .data({
            name: 'bhU',
            children: [
                {
                    name: 'bhava',
                    children: [
                        { name: 'bhavati' },
                        { name: 'bhavate' }
                    ]
                },
                {
                    name: 'bhaviSya',
                    children: [
                        { name: 'bhaviSyati' },
                        { name: 'bhaviSyate' }
                    ]
                }
            ]
        });
    tree('#bhu-simple-future');
});