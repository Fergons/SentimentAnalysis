// Created by Frantisek Sabol
import {error} from "@sveltejs/kit";
export async function load() {
    try {
        return {
            name: 'Home',
            subtitle: ''
        };
    } catch (err) {
        console.log(err);
        throw error(500, "Something went wrong.");
    }
}