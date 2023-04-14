import {error} from '@sveltejs/kit';
import type {PageLoad} from './$types';
import {GamesService} from "../../lib/client";

export const load: PageLoad = async ({params}) => {
    const [categories] = await Promise.all([
        GamesService.getCategoriesGamesSearchCategoriesGet()
    ]);
    return {
        categories: categories
    };

    throw error(404, 'Not found');
}