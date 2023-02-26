import {writable} from 'svelte/store';
import type {Source} from "../client";
export const sourcesStore = writable<Map<string,Source>>();
