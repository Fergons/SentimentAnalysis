import type { ReviewsSummaryDataPoint, Source } from "../client";

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

  if(data.length > 0){
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
      acc[nearestDate] = { ...initial, date: nearestDate };
    }

    acc[nearestDate][sourceName] += total;

    return acc;
  }, {} as Record<string, Record<string, any>>);

  const result: Record<string, any>[] = [];

  dateRange.forEach(date => {
    if (groupedByDate[date]) {
      result.push(groupedByDate[date]);
    } else {
      result.push({ ...initial, date });
    }
  });
  return result;
}