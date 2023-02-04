import { getGames } from '../../lib/server/api/games';
import { error } from '@sveltejs/kit';

export async function load() {
	const games1 = await getGames();
	return {
		games: games1
	};
}
