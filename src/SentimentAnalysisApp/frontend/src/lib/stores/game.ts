import {browser} from '$app/environment';
import {writable, readable} from 'svelte/store';
import type {GameListItem} from '../client';
import {GamesService} from "../client";
import {derived} from 'svelte/store';
import type {Writable} from 'svelte/store';
import {siWritedotas} from "simple-icons";


export type GameListFilter = {
    name?: string;
    categories?: string[];
    developers?: string[];
    minScore?: number;
    maxScore?: number;
    minNumReviews?: number;
    maxNumReviews?: number;
    minReleaseDate?: string;
    maxReleaseDate?: string;
}

export type GameListSort = {
    numReviews?: 'asc' | 'desc' | undefined;
    score?: 'asc' | 'desc' | undefined;
    releaseDate?: 'asc' | 'desc' | undefined;
}

export const initialGameFilterValue = {
    name: null,
    minNumReviews: null,
    maxNumReviews: null,
    minScore: null,
    maxScore: null,
    minReleaseDate: null,
    maxReleaseDate: null,
    categories: null,
    developers: null
} as unknown as GameListFilter;

export let loadingContent = writable(true)
export let moreContent = writable(false);
export const perPageLimit = 20;
export const gamePage = writable(0);
export const gameFilter = writable<GameListFilter>({...initialGameFilterValue})
export const gameSort = writable<GameListSort>({numReviews: 'desc'});
export const games = writable<GameListItem[]>();

export let selectedGame = writable<GameListItem>(undefined);


export const gameDataStore = derived(
    [gamePage, gameFilter, gameSort],
    // @ts-ignore
    async ([$gamePage, $gameFilter, $gameSort], set) => {
        loadingContent.set(true);
        const fetchedData = await getGames($gamePage, $gameFilter, $gameSort);
        if (fetchedData) {
            moreContent.set(fetchedData.total >= ($gamePage+1) * perPageLimit);
            set({
                // @ts-ignore
                games: fetchedData.games,
                total: fetchedData.total,
            });
        }
        loadingContent.set(false);
    },
    {games: [], total: 0}
);


export async function getGames(page: number, filter: GameListFilter, sort: GameListSort) {
    try {
        const offset = page * perPageLimit;
        if (filter.name === '') {
            filter.name = undefined;
        }
        const response = await GamesService.readGamesGamesGet(perPageLimit, offset,
            sort.numReviews, sort.score, sort.releaseDate,
            filter.name,
            filter.minNumReviews, filter.maxNumReviews, filter.minScore, filter.maxScore,
            filter.minReleaseDate, filter.maxReleaseDate,
            filter.categories ? filter.categories.join() : undefined,
            filter.developers ? filter.developers.join() : undefined);
        return {games: response.games, total: response.query_summary?.total || 0};
    } catch (e) {
        console.log(e);
        return {games: [], total: 0};
    }
}
