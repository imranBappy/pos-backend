import { USER_TYPE } from "../accounts/types";

interface RELATED_TYPE {
    id: string;
    name: string;
}

export interface DESCRIPTIONS {
    id: number,
    label: string
    description: string
    tag: string
}
export interface FAQ_TYPE {
    id: string,
    answer: string
    question: string
    product: PRODUCT_TYPE
}
export interface REVIEW_TYPE {
    id: string,
    rating: number
    content: string
    createdAt: Date
    product: PRODUCT_TYPE
    user: USER_TYPE

}
export interface ATTRIBUTE_OPTION_TYPE {
    id: number,
    option: string
    extraPrice: number
    message?: string
    photo?: string
}
export interface ATTRIBUTE_TYPE {
    id: string,
    name: string,
    attributeOptions?: {
        edges: { node: ATTRIBUTE_OPTION_TYPE }[]
    }
}

export interface PRODUCT_TYPE {
    id?: string;
    name: string;
    price: number;
    photo: string;
    sku: string;
    shortDescription: string;
    tag: string;
    isActive?: boolean;
    createdAt?: string;
    tax: number;
    priceRange?: string
    offerPrice?: number;

    category: RELATED_TYPE | string;
    subcategory: RELATED_TYPE | string;
    images: string,
    isTaxIncluded: boolean,
    attributes?: {
        edges: { node: ATTRIBUTE_TYPE }[]
    }
    descriptions?: {
        edges: { node: DESCRIPTIONS }[]
    }
    faqs?: {
        edges: { node: FAQ_TYPE }[]
    }
    reviews?: {
        edges: { node: REVIEW_TYPE }[]
    }
}
export interface CATEGORY_TYPE {
    id: string;
    name: string;
    description: string;
    photo: string;
    isActive: boolean;
    products?: PRODUCT_TYPE[];
    subcategories?: CATEGORY_TYPE[];
}

export interface SUBCATEGORY_TYPE {
    id: string;
    name: string;
    description: string;
    photo: string;
    isActive: boolean;
}

export interface ORDER_ITEM_TYPE {
    id: string;
    quantity: number;
    price: number;
    product: PRODUCT_TYPE;
}

export interface ADDRESS_TYPE {
    id: string;
    address: string;
    city: string;
    state: string;
    country: string;
    zip: string;
}

export interface ORDER_TYPE {
    id: string;
    user: USER_TYPE;
    paymentMethod: string;
    totalPrice: number;
    status: string;
    createdAt: string;
    items: PRODUCT_TYPE[];
    kitchen: RELATED_TYPE | string;
    category: RELATED_TYPE | string;
    subcategory: RELATED_TYPE | string;
    orderItems: ORDER_ITEM_TYPE[];
    address: ADDRESS_TYPE;
    type: string;
    orderId: string
}

export interface FLOOR_TYPE {
    name: string;
    id: string;
    createdAt: string,
    isActive: boolean,
    isBooked: boolean,

}

export interface FLOOR_TABLES_TYPE {
    name: string;
    id: string;
    createdAt: string,
    isActive: boolean,
    isBooked: boolean,
    floor: FLOOR_TYPE;
}

export interface PAYMENT_TYPE {
    id: string;
    user: USER_TYPE;
    paymentMethod: string;
    amount: number;
    status: string;
    createdAt: string;
    remarks: string;
    trxId: string;
    order: ORDER_TYPE[];
}




