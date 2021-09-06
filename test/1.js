function toFixed(n,digit=4){
    if(typeof n !== 'number' || typeof n !== 'number'){
        console.error(`${n} or ${digit} is not a number`) 
        return false
    }    
    if(Number.isInteger(n)) return n
    let arr = n.toString().split('.')
    let decimal = arr[1]
    if(digit>decimal.length){
        return `${arr[0]}.${decimal}`
    }else{
        let front = parseInt(decimal.substr(0,digit))
        return `${arr[0]}.${decimal[digit]>4?(front+1):front}`
    }
}
console.log(toFixed(8.85,0));