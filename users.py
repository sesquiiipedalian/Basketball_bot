import pandas


class Users:
    def __init__(self, df: pandas.DataFrame):
        self.df = df

    @staticmethod
    def from_file(path: str):
        try:
            return Users(pandas.read_csv(path))
        except FileNotFoundError:
            df = pandas.DataFrame({'user_id': []})
            df.to_csv(path, encoding='utf-8', index=False)
            return Users(df)

    def add_user(self, user_id: str):
        if self.df[self.df.user_id == user_id].empty:
            self.df = self.df.append({'user_id': user_id}, ignore_index=True)
            self.df.to_csv('users.csv', encoding='utf-8', index=False)

    def get_user_list(self):
        return self.df['user_id'].tolist()

    def delete_user(self, user_id):
        self.df = self.df[self.df.user_id != user_id]
        self.df.to_csv('users.csv', encoding='utf-8', index=False)


users = Users.from_file('users.csv')
