import { CalendarEvent } from '@/entities/Event';
import { createContext, ReactNode, useState } from 'react';

interface ModalContext {
  selectedEvent: CalendarEvent | null;
  setSelectedEvent: (event: CalendarEvent | null) => void;
}

export const ModalContext = createContext<ModalContext | null>(null);

export const ModalProvider = ({ children }: { children: ReactNode }) => {
  const [selectedEvent, setSelectedEvent] = useState<CalendarEvent | null>(null);

  return (
    <ModalContext.Provider value={{ selectedEvent, setSelectedEvent }}>
      {children}
    </ModalContext.Provider>
  );
};
