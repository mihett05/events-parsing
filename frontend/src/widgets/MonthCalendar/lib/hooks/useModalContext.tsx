import { useContext } from 'react';
import { ModalContext } from '../context/ModalContext';

export const useModalContext = () => {
  const context = useContext(ModalContext);
  return context;
};
