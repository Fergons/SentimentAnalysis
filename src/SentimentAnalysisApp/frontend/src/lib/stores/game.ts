import {browser} from '$app/environment';
import {writable, readable} from 'svelte/store';
import type {GameListItem} from '../client';
import {GamesService} from "../client";

export function initialValue() {
    return {
        games: new Map<number,GameListItem>(),
        loading: true
    }
}
const gameFilter = writable<Record<string, any>>({source: 'all'});
const gameSort = writable<string>('');

export function makeGameStore(args: any) {
    // 1. Build the store and initialize it as empty and error free
    let initial = initialValue();
    return readable(initial, makeSubscribe(initial, args));
}

function unsubscribe() {
    // Nothing to do in this case
}

function makeSubscribe(data: any, _args: any) {
    // 2. Create a closure with access to the
    // initial data and initialization arguments
    return (set: any) => {
        // 3. This won't get executed until the store has
        // its first subscriber. Kick off retrieval.
        fetchGameData(data, set);
        // 4. We're not waiting for the response.
        // Return the unsubscribe function which doesn't
        // do anything here (but is part of the stores protocol).
        return unsubscribe;
    };
}

async function fetchGameData(data: any, set: any) {
    try {
        // 5. Dispatch the request for the data
        const games = await GamesService.readGamesGamesGet()
         for (const {id, ...rest} of games) {
                data.games.set(id, {
                    id,
                    ...rest
                });
         }
         set(data);
    } catch (error) {
        // 6b. if there is a fetch error - deal with it
        console.log(error)
        data.error = error;
    } finally {
        // 6c. let observers know we're done loading
        // and let observers know
        data.loading = false;
        set(data);
    }
}