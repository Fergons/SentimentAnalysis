// Created by Frantisek Sabol
// implementation data transformation functions used to transform charts based on user input
import type {
    ReviewsSummaryDataPoint,
    Source,
    ReviewsSummaryV2,
    ReviewsSummaryByDate,
    ReviewsSummaryBaseDataPoint, AspectsSummary
} from "../client";
import {timeParse} from "d3-time-format";
import {
    timeDays, timeWeeks, timeMonths, timeYears,
    timeDay, timeWeek, timeMonth, timeYear
} from "d3-time";
import type {CountableTimeInterval} from "d3-time";
import {rgb} from "d3-color";
import type {CategoryPolarityCounts} from "../client";


function generateDates(actualDates: string[], parseDate: (s: string) => Date | null, timeInterval: CountableTimeInterval | null) {
    let dates: Date[];

    if (timeInterval) {
        const startDate = timeInterval.floor(parseDate(actualDates[0]) as Date);
        const endDate = timeInterval.ceil(parseDate(actualDates[actualDates.length - 1]) as Date);
        dates = timeInterval.range(startDate, endDate);
    } else {
        dates = actualDates.map((date) => parseDate(date) as Date);
    }
    return dates;
}

export function generateColorMap(
    selectedSources: string[],
    selectedTypes: string[],
    sourceColorMap: Map<string, string> | null,
    typeColorMap: Map<string, string> | null): Map<string, string> {
    // 8 pastel contrasting with grey and white and being primary blue
    const baseColors = [
        "#007bff",
        "#f28e2b",
        "#e15759",
        "#76b7b2",
        "#59a14f",
        "#edc948",
        "#b07aa1",
        "#ff9da7"
    ]

    const colorMap = new Map();

    let colorIndex = 0;
    for (const source of selectedSources) {
        const sourceColor = sourceColorMap ? sourceColorMap.get(source) || baseColors[colorIndex] : baseColors[colorIndex];
        colorMap.set(source, sourceColor);

        const sourceColorRgb = rgb(sourceColor);
        const typeShades = selectedTypes.map((_, i) => {
            const shadeFactor = 1 - (i + 1) * 0.1;
            return rgb(
                sourceColorRgb.r * shadeFactor,
                sourceColorRgb.g * shadeFactor,
                sourceColorRgb.b * shadeFactor
            ).toString();
        });

        let typeIndex = 0;
        for (const type of selectedTypes) {
            colorMap.set(`${source}_${type}`, typeShades[typeIndex]);
            typeIndex++;
        }

        colorIndex = (colorIndex + 1) % baseColors.length;
    }
    return colorMap;
}

export function transformSummary(
    summary: ReviewsSummaryV2,
    selectedSources: string[],
    selectedTypes: string[],
    sourceMap: Map<string, number>,
    timeInterval: CountableTimeInterval | null
): any[] {

    const selectedCounts = selectedSources.flatMap((source) => {
        return selectedTypes.flatMap((type) => `${source}_${type}`);
    });

    // create full result from sparse dates array
    const parseDate = timeParse("%Y-%m-%dT%H:%M:%S%Z");
    const actualDates = Object.keys(summary?.data || {});
    const dates = generateDates(actualDates, parseDate, timeInterval);

    //full result
    const result = dates.map(date => ({
        date,
        ...selectedCounts.reduce<Record<string, number>>((acc, count) => {
            acc[count] = 0;
            return acc;
        }, {})
    }));

    //inserting values to sparse result
    for (const strDate of actualDates) {
        const date = timeInterval ? timeInterval.floor(parseDate(strDate) as Date) : parseDate(strDate) as Date;
        const byDate = summary.data ? summary.data[strDate] : null;
        const sources = byDate ? byDate.sources : null;
        const dataPoint = result.find((point) => {
                return point.date.getTime() === date.getTime();
            }
        );
        if (dataPoint === undefined) continue;
        selectedSources.forEach((sourceName) => {
            if (sourceName === "all") {
                selectedTypes.forEach((type) => {
                    // @ts-ignore
                    dataPoint[`all_${type}`] += byDate ? byDate[type] : 0;
                });
            } else {
                const sourceId = sourceMap.get(sourceName);
                if (sourceId !== undefined && sources && sources[sourceId]) {
                    const sourceData = sources[sourceId] as { [key: string]: number };
                    selectedTypes.forEach((type) => {
                        // @ts-ignore
                        dataPoint[`${sourceName}_${type}`] += sourceData ? +sourceData[type] : 0;
                    });
                }
            }
        });
    }
    return result;
}


export function transformAspectSummary(data: Record<string, CategoryPolarityCounts>, timeInterval: CountableTimeInterval | null) {

    const parseDate = timeParse("%Y-%m-%dT%H:%M:%S%Z");
    const actualDates = Object.keys(data);
    const dates = generateDates(actualDates, parseDate, timeInterval);
    const polarities = ['positive', 'negative', 'neutral'];
    // find unique categories
    const categories = new Set<string>();
    for (const strDate of actualDates) {
        const categoriesForDate = data[strDate].categories;
        for (const category in categoriesForDate) {
            categories.add(category);
        }
    }
    const categoryDatasets = {};
    for (const category of categories) {
        // @ts-ignore
        categoryDatasets[category] = dates.map(date => ({date, positive: 0, negative: 0, neutral: 0}));
        for (const strDate of actualDates) {
            const date = timeInterval ? timeInterval.floor(parseDate(strDate) as Date) : parseDate(strDate) as Date;
            const byDate = data[strDate];
            const byCategory = byDate.categories;
            // @ts-ignore
            const dataPoint = categoryDatasets[category].find((point) => {
                    return point.date.getTime() === date.getTime();
                }
            );
            if (dataPoint === undefined) continue;
            for (const polarity of polarities) {
                // @ts-ignore
                dataPoint[polarity] += byCategory[category] ? byCategory[category][polarity] : 0;
            }
        }
    }
    return categoryDatasets;

}

