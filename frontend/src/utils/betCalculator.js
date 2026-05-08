export function calculatePayout(betAmount, odds) {
    const amount = parseFloat(betAmount)
    if (isNaN(amount) || amount <= 0) return 0

    let profit
    if (odds > 0) {
        profit = amount * (odds / 100)
    } else {
        profit = amount * (100 / Math.abs(odds))
    }

    return parseFloat((amount + profit).toFixed(2))
}