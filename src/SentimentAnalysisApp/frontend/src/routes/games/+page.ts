import {error} from '@sveltejs/kit';
import type {PageLoad} from './$types';
import {GamesService} from "../../lib/client";

export const load: PageLoad = async ({params}) => {
    const [categories, developers] = await Promise.all([
        GamesService.getCategoriesGamesSearchCategoriesGet(),
        GamesService.getDevelopersGamesSearchDevelopersGet()
    ]);
    return {
        categories: categories,
        developers: developers
    };

    throw error(404, 'Not found');
}