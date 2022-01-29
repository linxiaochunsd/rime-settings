local function translator(input, seg)
   if (input == "riqi") then
      --- Candidate(type, start, end, text, comment)
      local cand = Candidate("date", seg.start, seg._end, os.date("%Y年%m月%d日"), "〔日期〕")
      cand.quality = 0.3
      yield(cand)

      local cand = Candidate("date", seg.start, seg._end, os.date("%Y-%m-%d"), "〔日期〕")
      cand.quality = 0.3
      yield(cand)
   end
   if (input == "riqiuijm") then
      local cand = Candidate("time", seg.start, seg._end, table.concat({os.date("%Y年%m月%d日 "),os.date("%H:%M:%S")}), "〔日期时间〕")
      cand.quality = 0.1
      yield(cand)

      local cand = Candidate("time", seg.start, seg._end, table.concat({os.date("%Y-%m-%d "),os.date("%H:%M:%S")}), "〔日期时间〕")
      cand.quality = 0.1
      yield(cand)
   end

   if (input == "uijm") then
      local cand = Candidate("time", seg.start, seg._end, os.date("%H:%M:%S"), "〔时间〕")
      cand.quality = 0.1
      yield(cand)
   end
end

return translator
