export interface CalendarEvent {
  id: number;
  title: string;
  startDate: Date;
  endDate?: Date;
  isMultiDay?: boolean;
  description: string;
  type: "hackaton" | "conference" | "other";
  format: "online" | "offline" | "hybrid";
  color: string;
}
