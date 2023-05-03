import {error} from '@sveltejs/kit';
import {GamesService} from "../../lib/client";

export async function load() {
    try {
        const [categories, developers] = await Promise.all([
            GamesService.getCategoriesGamesSearchCategoriesGet(),
            GamesService.getDevelopersGamesSearchDevelopersGet()
        ]);
        return {
            name: 'Games',
            subtitle: '',
            categories: categories,
            developers: developers
        };
    } catch (err) {
        console.log(err);
        throw error(500, "Something went wrong.");
    }
}
