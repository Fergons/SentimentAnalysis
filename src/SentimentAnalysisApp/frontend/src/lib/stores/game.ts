import {browser} from '$app/environment';
import {writable, readable} from 'svelte/store';
import type {GameListItem} from '../client';
import {GamesService} from "../client";
import {derived} from 'svelte/store';
import type {Readable} from 'svelte/store';


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

export function applyGameFilter(game: GameListItem, filter: GameListFilter): boolean {
    // Add your filter logic here. This is just an example.
    const {
        name,
        categories,
        developers,
        minScore: min_score,
        maxScore: max_score,
        minNumReviews: min_num_reviews,
        maxNumReviews: max_num_reviews,
        minReleaseDate: min_release_date,
        maxReleaseDate: max_release_date,
    } = filter;
    const matchesName = name ? game.name.toLowerCase().includes(name.toLowerCase()) : true;
    const matchesCategory = categories ?
        categories.some((category) => game.categories.includes(category)) : true;
    const matchesDeveloper = developers ?
        developers.some((developer) => game.developers.includes(developer)) : true;
    const matchesScore = game.score ?
        min_score ? +game.score >= min_score : max_score ? +game.score <= max_score : true : true;
    const matchesNumReviews = min_num_reviews ?
        game.num_reviews >= min_num_reviews : max_num_reviews ? game.num_reviews <= max_num_reviews : true;
    const matchesReleaseDate = game.release_date ?
        min_release_date ? new Date(game.release_date).getTime() >= new Date(min_release_date).getTime() :
            max_release_date ? new Date(game.release_date).getTime() <= new Date(max_release_date).getTime() : true : true;
    return matchesName && matchesCategory && matchesDeveloper && matchesScore && matchesNumReviews && matchesReleaseDate;
}

