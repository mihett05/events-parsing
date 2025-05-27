import { api, UserModel, UserRoleModel } from '@/shared/api/api';
import { setToken } from '@/shared/api/tokens';
import { createSlice } from '@reduxjs/toolkit';

interface UserState {
  user: UserModel | null;
  organizations: UserRoleModel[];
}

const initialState: UserState = {
  user: null,
  organizations: [],
};

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addMatcher(api.endpoints.loginUserV1AuthLoginPost.matchFulfilled, (state, { payload }) => {
        state.user = payload.user;
        setToken(payload.accessToken);
      })
      .addMatcher(
        api.endpoints.readUserRolesV1UsersRolesUserIdGet.matchFulfilled,
        (state, { payload }) => {
          state.organizations = payload;
        },
      )
      .addMatcher(api.endpoints.getMeV1UsersMeGet.matchFulfilled, (state, { payload }) => {
        state.user = payload;
      });
  },
});

export const {} = userSlice.actions;
export default userSlice.reducer;
