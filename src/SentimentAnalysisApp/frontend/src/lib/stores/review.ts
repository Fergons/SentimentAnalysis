import {writable, readable, derived} from 'svelte/store';
import {ReviewsService} from "../client";
import type {ReviewsSummary, ReviewsSummaryDataPoint} from '../client';

type SummaryFilterType = {
    source?: Array<string>;
    dateStart?: string;
    dateEnd?: string;
    type?: string;
}

function initialValue() {
    return {
        reviewsSummary: null,
        loading: true
    }
}

const summaryFilter = writable<SummaryFilterType>({});
const summarySort = writable<string>('');
const reviewsSummaryStore = writable<ReviewsSummary>();

const reviewsSummaryFiltered = derived([summaryFilter, reviewsSummaryStore],
    ([$summaryFilter, $reviewsSummaryStore]) => {
    // TODO: Implement filtering
})