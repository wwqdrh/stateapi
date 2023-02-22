## 简介

用于处理动态模型

## orm

使用http/grpc进行数据交互
- 创建table
- 数据插入
- 数据查询
- 分组查询
- 数据修改

- /orm/:app/create;body={tablename: "", fields: []}
- /orm/:app/:table/insert;body={values: [{name: '', value: '', mode: ''}]}
- /orm/:app/:table/query;body={query: [{left: '', op: '', right: ''}]}

## 环境问题

1、手动管理使用grpc
2、使用dapr的grpc端点
