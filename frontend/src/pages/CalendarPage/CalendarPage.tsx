import { Layout } from '@/shared/ui/Layout';
import { MonthCalendar } from '@widgets/MonthCalendar';
import { DayCalendar } from '@/widgets/DayCalendar';
import { YearCalendar } from '@/widgets/YearCalendar';
import { ModalProvider } from '@/widgets/MonthCalendar/lib/context/ModalContext';
import { EventDetailsModal } from '@/widgets/MonthCalendar/ui/EventDetailsModal';
import LoadingIndicator from '@/shared/ui/LoadingIndicator';
import { CalendarControlProps } from '@/widgets/CalendarCommon/types';
import { useCalendarPageController } from './hooks/useCalendarPageController';

export const CalendarPage = () => {
  const {
    currentCalendarView,
    currentDate,
    activeFilters,
    handleNavigation,
    isInitialRedirectNeeded,
  } = useCalendarPageController();

  if (isInitialRedirectNeeded) {
    return (
      <Layout>
        <LoadingIndicator />
      </Layout>
    );
  }

  const calendarProps: CalendarControlProps = {
    currentCalendarView,
    currentDate,
    activeFilters,
    onNavigate: handleNavigation,
  };

  const renderCalendarView = () => {
    switch (currentCalendarView) {
      case 'day':
        return <DayCalendar {...calendarProps} />;
      case 'year':
        return <YearCalendar {...calendarProps} />;
      case 'month':
      default:
        return <MonthCalendar {...calendarProps} />;
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
