export interface CalendarEvent {
  id: string | number;
  title: string;
  color: string;
  startDate: Date;
  endDate?: Date;
  isMultiDay?: boolean;
}
