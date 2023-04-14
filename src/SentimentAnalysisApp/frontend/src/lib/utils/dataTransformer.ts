import type {
    ReviewsSummaryDataPoint,
    Source,
    ReviewsSummaryV2,
    ReviewsSummaryByDate,
    ReviewsSummaryBaseDataPoint
} from "../client";
import {timeFormat, timeParse} from "d3-time-format";
import {
    timeDays, timeWeeks, timeMonths, timeYears,
    timeDay, timeWeek, timeMonth, timeYear
} from "d3-time";
import type {CountableTimeInterval} from "d3-time";
import {rgb} from "d3-color";

function generateDateRange(startDate: Date, endDate: Date, numberOfPoints: number): string[] {
    const timeDiff = endDate.getTime() - startDate.getTime();
    const interval = timeDiff / (numberOfPoints - 1);
    const dateRange: string[] = [];

    for (let i = 0; i < numberOfPoints; i++) {
        const date = new Date(startDate.getTime() + interval * i);
        dateRange.push(date.toISOString().split(".")[0] + "Z");
    }

    return dateRange;
}

function findNearestDate(date: string, dateRange: string[]): string {
    const target = new Date(date).getTime();
    const nearestDate = dateRange.reduce((prev, curr) =>
        Math.abs(new Date(curr).getTime() - target) < Math.abs(new Date(prev).getTime() - target) ? curr : prev
    );
    return nearestDate;
}

export function getTotal(data: ReviewsSummaryDataPoint[], sources: Map<number, Source>, numberOfPoints: number = 30) {
    const initial: Record<string, number> = {};

    for (const [key, value] of sources) {
        initial[value.name] = 0;
    }


    data.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
    let minDate = null;
    let maxDate = null;

    if (data.length > 0) {
        minDate = new Date(data[0].date);
        maxDate = new Date(data[data.length - 1].date);
    } else {
        minDate = new Date();
        maxDate = new Date();
        maxDate.setDate(maxDate.getDate() + 30);
    }

    const dateRange = generateDateRange(minDate, maxDate, numberOfPoints);

    const groupedByDate = data.reduce((acc, obj) => {
        const date = obj.date;
        const sourceId = obj.source_id;
        const total = obj.total;
        const sourceName = sources.get(sourceId)?.name;

        if (!sourceName) return acc;

        const nearestDate = findNearestDate(date, dateRange);

        if (!acc[nearestDate]) {
            acc[nearestDate] = {...initial, date: nearestDate};
        }

        acc[nearestDate][sourceName] += total;

        return acc;
    }, {} as Record<string, Record<string, any>>);

    const result: Record<string, any>[] = [];

    dateRange.forEach(date => {
        if (groupedByDate[date]) {
            result.push(groupedByDate[date]);
        } else {
            result.push({...initial, date});
        }
    });
    return result;
}

export function generateColorMap(
    selectedSources: string[],
    selectedTypes: string[],
    sourceColorMap: Map<string, string>|null,
    typeColorMap: Map<string, string>|null): Map<string, string> {
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
    let dates: Date[];
    if (timeInterval) {
        const startDate = timeInterval.floor(parseDate(actualDates[0]) as Date);
        const endDate = timeInterval.ceil(parseDate(actualDates[actualDates.length - 1]) as Date);
        dates = timeInterval.range(startDate, endDate);
    } else {
        dates = actualDates.map((date) => parseDate(date) as Date);
    }

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

