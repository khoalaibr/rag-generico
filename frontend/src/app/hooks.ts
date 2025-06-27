// frontend/src/app/hooks.ts
import { useDispatch, useSelector, TypedUseSelectorHook } from 'react-redux';
import type { RootState, AppDispatch } from './store';

// Crea versiones tipadas de los hooks de Redux.
// No es necesario que entiendas esto en profundidad, solo úsalos
// en lugar de los `useDispatch` y `useSelector` estándar.

export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
