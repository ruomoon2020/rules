# Dependency Governance

1. 新增依赖须说明用途、许可证、体积与安全影响。
2. 定期 OWASP dependency-check 或 GitHub Dependabot。
3. Spring Boot BOM 对齐；禁止随意升级 major 无回归。
4. MyBatis-Plus、驱动（mysql、postgresql）版本在父 POM 统一管理。
