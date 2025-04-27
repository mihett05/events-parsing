export interface CalendarEvent {
  id: number;
  title: string;
  startDate: Date;
  endDate?: Date;
  isMultiDay?: boolean;
  description: string;
  type: string;
  format: string;
  color: string;
  endRegistration?: Date;
}
