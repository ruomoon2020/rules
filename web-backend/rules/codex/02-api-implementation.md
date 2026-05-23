# API Implementation Flow

新接口推荐顺序：

```text
1. 更新 contracts/openapi.yaml
2. 定义 Request / Response DTO（或生成）
3. Controller：@Valid、鉴权、调用 Service
4. Application Service：@Transactional、业务逻辑、DTO 映射
5. Mapper / XML：数据访问
6. MockMvc / 集成测试
7. openapi-diff + archunit
```

分页列表须用 MP `Page` + `19-pagination-query` 白名单排序。
