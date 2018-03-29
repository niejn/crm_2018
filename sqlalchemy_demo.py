def sync_qiquanzuoshi(self, t_date='20170630'):
    constr = self.__sou_constr
    # 更换为position
    # 增加etfposition
    # table_etfposition = 'ETFPOSITION'
    table_position = 'POSITION'
    table_qiquanzuoshi = 'G_OPTION_DEALER'
    table_task = 'T_OWN_INVEST_DERIV'
    table_position = table_position.lower()
    table_qiquanzuoshi = table_qiquanzuoshi.lower()
    table_task = table_task.lower()
    test_time = datetime.now()
    # print(test_time)
    engine = self.get_engine(constr)

    # meta = MetaData(bind=engine, reflect=True)
    # position = meta.tables[table_position]
    # dealer = meta.tables[table_qiquanzuoshi]
    # task_deriv = meta.tables[table_task]
    meta = MetaData(bind=engine)
    position = Table(table_position.lower(), meta, autoload=True)
    dealer = Table(table_qiquanzuoshi.lower(), meta, autoload=True)
    # added on 2017-10-12
    # etfposition = Table(table_position.lower(), meta, autoload=True)

    task_deriv = Table(table_task.lower(), meta, autoload=True)

    # 删除在从期权做市表中查询的dealer.c.the_main_contract
    columns = [dealer.c.report_date, dealer.c.manage_company_code, dealer.c.derivatives_type, dealer.c.on_exchange_flag, \
               dealer.c.exchange_type, dealer.c.counter_party, dealer.c.cp_cred_type, dealer.c.cp_cred_id, \
               dealer.c.cp_inter_rating, dealer.c.the_main_contract, position.c.notional_value,
               position.c.premium_price, \
               position.c.delta_value, position.c.press_loss, position.c.book_value, dealer.c.currency_code, \
               dealer.c.group_inter_trans_flag, dealer.c.group_counter_party, dealer.c.group_counter_value, \
               dealer.c.last_modified_date]

    # 删除LAST_MODIFIED_DATE
    t_keys = ['report_date', 'manage_company_code', 'derivatives_type', 'on_exchange_flag',
              'exchange_type', 'counter_party', 'cp_cred_type', 'cp_cred_id', 'cp_inter_rating',
              'currency_code', 'group_inter_trans_flag', 'group_counter_party',
              'group_counter_value',
              'notional_value',
              'premium_price', 'delta_value', 'press_loss',
              'hold_asset', 'book_value',
              # 在持仓表中增加持仓手数和买卖方向两个字段
              'lots', 'direction'
              ]

    # ----------------------------
    Session = sessionmaker(bind=engine)
    session = Session()
    # dealer_first = session.query(dealer).first()
    # position_all = session.query(position).all()

    # 删除LAST_MODIFIED_DATE
    # 删除在从期权做市表中查询的dealer.c.the_main_contract
    # dealer_task_15 = session.query(dealer.c.report_date, dealer.c.manage_company_code, dealer.c.derivatives_type, dealer.c.on_exchange_flag, \
    # dealer.c.exchange_type, dealer.c.counter_party, dealer.c.cp_cred_type, dealer.c.cp_cred_id, \
    # dealer.c.cp_inter_rating, dealer.c.currency_code, \
    # dealer.c.group_inter_trans_flag, dealer.c.group_counter_party, dealer.c.group_counter_value).all()
    # where(o_table.c.trading_day == (t_date))

    # t_date = '20170630'
    dealer_task_15 = session.query(dealer.c.report_date, dealer.c.manage_company_code, dealer.c.derivatives_type,
                                   dealer.c.on_exchange_flag, \
                                   dealer.c.exchange_type, dealer.c.counter_party, dealer.c.cp_cred_type,
                                   dealer.c.cp_cred_id, \
                                   dealer.c.cp_inter_rating, dealer.c.currency_code, \
                                   dealer.c.group_inter_trans_flag, dealer.c.group_counter_party,
                                   dealer.c.group_counter_value).filter(dealer.c.report_date == (t_date)).all()

    # trading_day == (t_date) 2017-06-30
    position_task_5 = session.query(position.c.notional_value, position.c.premium_price, \
                                    position.c.delta_value, position.c.press_loss,
                                    position.c.hold_asset, position.c.book_value,
                                    # 在持仓表中增加持仓手数和买卖方向两个字段
                                    position.c.lots, position.c.direction

                                    ).filter(position.c.report_date == (t_date)).all()
    ans_tasks = []

    def row2dict(row):
        d = {}
        for column in row._fields:
            d[str(column)] = row[column]

        return d

    tt = dealer_task_15[0]
    cols = [str(column) for column in tt._real_fields]
    vals = list(dealer_task_15[0])
    a_dealer_task_15 = dict(zip(cols, vals))

    for a_position in position_task_5:
        #   --TARGET_PRICE修改为衍生品表中对应字段名字book_value
        # temp_target_price = a_position.target_price
        temp_target_price = a_position.book_value
        a_position_cols = [str(column) for column in a_position._real_fields]
        a_position_vals = list(a_position)
        a_position_dict = dict(zip(a_position_cols, a_position_vals))
        # 持仓查询excel文件：
        # 标的价格为0——期货，
        # 标的价格！=0——期权
        # 判断是否是期货，期货填D13，否则d14
        # temp = a_dealer_task_15.derivatives_type
        # a_dealer_task_15.derivatives_type = 'D13'
        if temp_target_price == 0:
            a_dealer_task_15['derivatives_type'] = 'D13'
        else:
            a_dealer_task_15['derivatives_type'] = 'D14'

        # 标的价格
        a_task = {}
        a_task.update(a_dealer_task_15)
        a_task.update(a_position_dict)
        ans_tasks.append(a_task)

    final_task = ans_tasks
    ans = self.insert_direct(constr=constr, tablename=table_task, data_list=final_task)

    return ans


def get_db(self, constr=None, tar_table=None):
    tar_table = tar_table.lower()
    test_time = datetime.now()
    print(test_time)
    engine = self.get_engine(constr)

    # meta = MetaData(bind=engine, reflect=True)
    # table = meta.tables[tar_table]

    # on0922, 优化反射，不反射整个数据库
    meta = MetaData(bind=engine)
    table = Table(tar_table.lower(), meta, autoload=True)

    result = list(engine.execute(table.select()))
    # print(result)

    return result

from pandas.io import sql
#cnx = engine.connect().connection # option-1
cnx = engine.raw_connection() # option-2
xx = sql.read_frame("SELECT * FROM user", cnx)
cnx.close()

# Just to make this more clear for novice pandas programmers, here is a concrete example,
#
# pd.read_sql(session.query(Complaint).filter(Complaint.id == 2).statement,session.bind)
# Here we select a complaint from complaints table (sqlalchemy model is Complaint) with id = 2

# If
# you
# want
# to
# compile
# a
# query
# with parameters and dialect specific arguments, use something like this:

# c = query.statement.compile(query.session.bind)
# df = pandas.read_sql(c.string, query.session.bind, params=c.params)
#
#
# Below should work in most cases:
#
# df = pd.read_sql(query.statement, query.session.bind)
