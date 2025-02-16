


const product = {
    id: 1,
    name: "HP Laptop 405G",
    price: 150,
    shortDescription: "short description.....",
    descriptions: [
        {
            id: 1,
            label: "Description",
            tag: "#description",
            description: "description 1.....",
        },
        {
            id: 2,
            label: "Specification",
            tag: "#specification",
            description: "description 2.....",
        }
    ],

    attributes: [
        {
            id: 1,
            name: "Version",
            options: [
                {
                    id: 1,
                    option: "Version 1",
                    price: 150,

                },
                {
                    id: 1,
                    option: "Version 2",
                    price: 0,
                }
            ]
        }
    ],


    reviews: [
        {
            userId: 1,
            start: '5',
            command: 'This is best product ever'
        },
        {
            userId: 2,
            start: '4.5',
            command: 'This is best product ever'
        },
        {
            userId: 3,
            start: '3',
            command: 'This is best product ever'
        }
    ]
}

console.log(product);
