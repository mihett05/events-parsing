import { Layout } from '@/shared/ui/Layout';
import { MonthCalendar } from '@widgets/MonthCalendar';
import { DayCalendar } from '@/widgets/DayCalendar';
import { YearCalendar } from '@/widgets/YearCalendar';
import { useAppSelector } from '@/shared/store/hooks';
import { selectCalendarView } from '@/features/events/slice';
import { ModalProvider } from '@/widgets/MonthCalendar/lib/context/ModalContext';
import { EventDetailsModal } from '@/widgets/MonthCalendar/ui/EventDetailsModal';

export const CalendarPage: React.FC = () => {
  const currentView = useAppSelector(selectCalendarView);

  const renderCalendarView = () => {
    switch (currentView) {
      case 'day':
        return <DayCalendar />;
      case 'year':
        return <YearCalendar />;
      case 'month':
      default:
        return <MonthCalendar />;
    }
  };

  return (
    <Layout>
      <ModalProvider>
        {renderCalendarView()}
        <EventDetailsModal />
      </ModalProvider>
    </Layout>
  );
};
