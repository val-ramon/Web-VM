function range(start, end) {
    var ans = [];
    for (let i = start; i <= end; i++) {
        ans.push(i);
    }
    return ans;
} 
for (var j = 0; j < source.data.RT.length; j++){
    source.data.RT_intensity[j] = range(0, 49);
}
source.change.emit();