# Contributing to MT Expert Optimizer

Thank you for your interest in contributing! 🎉

## Development Workflow

1. **Fork** the repository
2. **Clone** your fork
3. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
4. **Make** your changes
5. **Test** your changes
6. **Commit** your changes (following commit conventions below)
7. **Push** to your fork
8. **Submit** a Pull Request

## Commit Conventions

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: Add new feature
fix: Bug fix
docs: Documentation changes
style: Code formatting (no functional changes)
refactor: Code refactoring
test: Add or update tests
chore: Build/config changes
perf: Performance improvements
```

### Examples

```bash
git commit -m "feat: add genetic algorithm optimization"
git commit -m "fix: resolve MT5 terminal connection issue"
git commit -m "docs: update API documentation"
```

## Code Style

### Python (Backend)
- Follow PEP 8
- Use Black for formatting
- Use type hints
- Write docstrings

```python
def calculate_profit_factor(gross_profit: float, gross_loss: float) -> float:
    """
    Calculate profit factor metric

    Args:
        gross_profit: Total profit from winning trades
        gross_loss: Total loss from losing trades

    Returns:
        Profit factor (gross_profit / gross_loss)
    """
    if gross_loss == 0:
        return 0.0
    return gross_profit / abs(gross_loss)
```

### TypeScript (Frontend)
- Use TypeScript strict mode
- Use ESLint + Prettier
- Follow React best practices

```typescript
interface BacktestResult {
  id: string;
  profit: number;
  profitFactor: number;
  sharpeRatio: number;
}

const BacktestCard: React.FC<{ result: BacktestResult }> = ({ result }) => {
  return (
    <div className="border rounded-lg p-4">
      <h3>{result.id}</h3>
      <p>Profit: ${result.profit}</p>
    </div>
  );
};
```

## Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=app tests/
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

## Pull Request Guidelines

1. **Update documentation** if adding new features
2. **Add tests** for new functionality
3. **Ensure all tests pass**
4. **Keep PRs focused** - one feature per PR
5. **Write clear PR descriptions**

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How has this been tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests passing
```

## Development Setup

See [README.md](README.md) for detailed setup instructions.

## Questions?

- Open an issue for bugs
- Start a discussion for feature requests
- Join our Discord for questions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
