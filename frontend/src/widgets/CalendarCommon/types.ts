import { CalendarView, FilterState } from '@/features/events/slice';

export interface CalendarNavOptions {
  view?: CalendarView;
  date?: Date;
  filters?: Partial<FilterState>;
}
export interface CalendarControlProps {
  currentCalendarView: CalendarView;
  currentDate: Date;
  activeFilters: FilterState;
  onNavigate: (options: CalendarNavOptions) => void;
}
