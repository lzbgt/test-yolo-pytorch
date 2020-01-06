import numpy as np
import os, sys, random

def prepare(src_dir, target_dir):
  data = np.loadtxt(src_dir + '/message_for_person.csv', dtype='U512,int,int,int,int,int', delimiter=',',unpack=False)
  lastName = None
  lines = []
  names = []
  for row in data:
    shortName = row[0][row[0].rindex('/') + 1:]
    if lastName != shortName:
      names.append(shortName)
      if len(lines) > 0: # write last
        os.symlink(src_dir + '/' + row[0], target_dir + '/images/' + shortName)
        if lastName:
          tmpName = target_dir + '/labels/' + lastName.replace('.png', '.txt')
          with open(tmpName, "w") as f:
            f.write('\n'.join(lines))
      lines = []
      lastName = shortName
    line = "{} {} {} {} {}".format(row[5],(row[3] + row[1])//2, (row[4] + row[2])//2, row[3]- row[1], row[4] - row[2]);
    lines.append(line)

  if len(lines) > 0: # write last
    tmpName = target_dir + '/labels/' + lastName.replace('.png', '.txt')
    with open(tmpName, "w") as f:
      f.write('\n'.join(lines))
  
  names = ['data/custom/images/' + x for x in names]
  random.shuffle(names)
  ridx = int(len(names)*0.8)
  with open(target_dir + '/train.txt', 'w') as f:
    f.write('\n'.join(names[:ridx]))

  with open(target_dir + '/valid.txt', 'w') as f:
    f.write('\n'.join( names[ridx:]))


if __name__ == "__main__":
  os.system("mkdir -p {}; mkdir -p {}/images; mkdir -p {}/labels".format(sys.argv[1], sys.argv[2],sys.argv[2]))
  prepare(sys.argv[1], sys.argv[2])


